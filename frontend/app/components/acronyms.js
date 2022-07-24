import Component from '@glimmer/component';
import { service } from '@ember/service';
import { tracked } from '@glimmer/tracking';
import { task, taskGroup, timeout } from 'ember-concurrency';

export default class AcronymsComponent extends Component {
  @service store;
  @tracked display_per_page = 3;
  @tracked page = 1;
  @tracked columns = [];
  @tracked acronyms = [];
  @tracked has_next = true;
  @tracked has_prev = false;
  @tracked pages_count = 1;
  @taskGroup({ drop: true }) changes;

  constructor(...args) {
    super(...args);
    let { columns } = this.args;
    this.columns = columns;
    this.update.perform();
  }

  @task({ drop: true })
  *update() {
    yield this.store
      .query('acronym', {
        display_per_page: this.display_per_page,
        page: this.page,
      })
      .then((results) => {
        this.has_next = results.meta.has_next;
        this.has_prev = results.meta.has_prev;
        this.pages_count = results.meta.pagesCount;
        this.acronyms = results;
      });
    yield timeout(150);
  }

  @task({ group: 'changes' })
  *changeDisplayPerPage(event) {
    this.display_per_page = parseInt(event.target.value);
    this.page = 1;
    yield this.update.perform();
  }

  @task({ group: 'changes' })
  *changePage(event) {
    this.page = parseInt(event.target.value);
    yield this.update.perform();
  }

  @task({ group: 'changes' })
  *next_page() {
    this.page += 1;
    yield this.update.perform();
  }

  @task({ group: 'changes' })
  *prev_page() {
    this.page -= 1;
    yield this.update.perform();
  }

  @task({ group: 'changes' })
  *first_page() {
    this.page = 1;
    yield this.update.perform();
  }

  @task({ group: 'changes' })
  *last_page() {
    this.page = this.pages_count;
    yield this.update.perform();
  }

  @task({ group: 'changes' })
  *changeColumn(columnName) {
    let newColumns = JSON.parse(JSON.stringify(this.columns));
    yield newColumns.forEach((column) => {
      if (column.property === columnName) {
        column.enabled = !column.enabled;
      }
    });
    this.columns = newColumns;
  }
}
