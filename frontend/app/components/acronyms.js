import Component from '@glimmer/component';
import { action } from '@ember/object';
import { service } from '@ember/service';
import { tracked } from '@glimmer/tracking';
// import { computed } from '@ember/object';

export default class AcronymsComponent extends Component {
  @service store;
  @tracked display_per_page = 3;
  @tracked page = 1;
  @tracked acronyms = null;
  @tracked has_next = true;
  @tracked has_prev = false;
  //   @computed('display_per_page', 'page', 'store')
  constructor(...args) {
    super(...args);
    this.update();
  }

  @action
  async update() {
    this.store
      .query('acronym', {
        display_per_page: this.display_per_page,
        page: this.page,
      })
      .then((results) => {
        this.has_next = results.meta.has_next;
        this.has_prev = results.meta.has_prev;
        this.acronyms = results;
      });
  }

  @action
  changeDisplayPerPage(event) {
    this.display_per_page = event.target.value;
    this.update();
  }

  @action
  next_page() {
    this.page += 1;
    this.update();
  }

  @action
  prev_page() {
    this.page -= 1;
    this.update();
  }
}
