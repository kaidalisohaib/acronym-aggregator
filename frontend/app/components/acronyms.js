import Component from '@glimmer/component';
import { service } from '@ember/service';
import { tracked } from '@glimmer/tracking';
import { task, taskGroup, timeout } from 'ember-concurrency';
import { action } from '@ember/object';
export default class AcronymsComponent extends Component {
  @service store;
  @tracked display_per_page = 3;
  @tracked page = 1;
  @tracked columns = [];
  @tracked acronyms = [];
  @tracked has_next = true;
  @tracked has_prev = false;
  @tracked pages_count = 1;
  @tracked sorting_column = null;
  @tracked sorting_ascending = null;
  @taskGroup({ drop: true }) changes;

  constructor(...args) {
    super(...args);
    let { columns } = this.args;
    columns.forEach((column) => {
      if (!('query' in column)) {
        column.query = null;
      }
    });
    this.columns = columns;
    this.update.perform();
  }

  /**
   * This function fetchs the data from the backend with all
   * the parameters needed and is called after each changement.
   */
  @task({ drop: true })
  *update() {
    // Preparing the optional queries
    let filter = {};
    this.columns.forEach((column) => {
      if (column.query && column.query.trim()) {
        filter[column.property] = column.query;
      }
    });
    let sorting = {};
    if (this.sorting_column) {
      sorting['column'] = this.sorting_column;
    }
    if (this.sorting_ascending !== null) {
      sorting['ascending'] = this.sorting_ascending;
    }

    yield this.store
      .query('acronym', {
        display_per_page: this.display_per_page,
        page: this.page,
        filter: filter,
        sorting: sorting,
      })
      .then((results) => {
        this.has_next = results.meta.has_next;
        this.has_prev = results.meta.has_prev;
        this.pages_count = results.meta.pages_count;
        this.acronyms = results;
      });
    yield timeout(150);
  }

  /**
   * Change the number of acronym per page
   * @param {*} event Event of the select html object so we can get his value
   */
  @task({ group: 'changes' })
  *changeDisplayPerPage(event) {
    let last_page = this.page;
    let last_display_per_page = this.display_per_page;
    this.display_per_page = parseInt(event.target.value);
    this.page = 1;
    yield this.update.perform().catch(() => {
      this.page = last_page;
      this.display_per_page = last_display_per_page;
    });
  }

  /**
   * Go to the selected page
   * @param {*} event Event of the select html object so we can get his value
   */
  @task({ group: 'changes' })
  *changePage(event) {
    let last_page = this.page;
    this.page = parseInt(event.target.value);
    yield this.update.perform().catch(() => (this.page = last_page));
  }
  /**
   * Go to the next page
   */
  @task({ group: 'changes' })
  *next_page() {
    let last_page = this.page;
    this.page += 1;
    yield this.update.perform().catch(() => (this.page = last_page));
  }

  /**
   * Go to the previous page
   */
  @task({ group: 'changes' })
  *prev_page() {
    let last_page = this.page;
    this.page -= 1;
    yield this.update.perform().catch(() => (this.page = last_page));
  }

  /**
   * Go to the first page
   */
  @task({ group: 'changes' })
  *first_page() {
    let last_page = this.page;
    this.page = 1;
    yield this.update.perform().catch(() => (this.page = last_page));
  }

  /**
   * Go to the last page
   */
  @task({ group: 'changes' })
  *last_page() {
    let last_page = this.page;
    this.page = this.pages_count;
    yield this.update.perform().catch(() => (this.page = last_page));
  }

  /**
   * Show/Hide the column of the buttonn pressed
   * @param {*} columnProperty The column property name to Show/Hide
   */
  @task({ group: 'changes' })
  *toggleColumn(column) {
    column.enabled = !column.enabled;
    if (!column.enabled) {
      column.query = null;
    }
    yield this.changeColumns(this.columns);
  }

  /**
   * Remove the text within a query input if the 'X' button was pressed
   * @param {*} columnProperty The column property name to remove the query
   */
  @task({ group: 'changes' })
  *clearQuery(column) {
    column.query = null;
    this.changeColumns(this.columns);
    this.page = 1;
    yield this.update.perform();
  }

  @task({ group: 'changes' })
  *searchQuery() {
    let queryEmpty = true;
    for (const column of this.columns) {
      if (column.query && column.query.trim()) {
        queryEmpty = false;
        break;
      }
    }
    if (!queryEmpty) {
      this.page = 1;
      yield this.update.perform();
    }
  }

  @task({ group: 'changes' })
  *changeSorting(column) {
    if (this.sorting_column === column.property) {
      if (this.sorting_ascending) {
        this.sorting_ascending = false;
      } else {
        this.sorting_column = null;
        this.sorting_ascending = null;
      }
    } else {
      this.sorting_column = column.property;
      this.sorting_ascending = true;
    }
    console.log(column);
    console.log(this.sorting_column + '       ' + this.sorting_ascending);
    yield this.update.perform();
  }

  /**
   * This function was made to update all related html attributes and component related to this.columns.
   * Since emberjs doesn't track array elements, we need to update the whole array pointer to update the template.
   * @param {*} new_columns New version of the columns array
   */
  changeColumns(new_columns) {
    this.columns = JSON.parse(JSON.stringify(new_columns));
  }

  @action
  handleChecklistMenu(event) {
    event.stopPropagation();
  }
}
