import Component from '@glimmer/component';
import { service } from '@ember/service';
import { tracked } from '@glimmer/tracking';
import { task, taskGroup, timeout } from 'ember-concurrency';
import { action } from '@ember/object';
import { guidFor } from '@ember/object/internals';

/**
 * Table with multiple functionalities.
 * Filter by column: Contains the text.
 */
export default class AcronymsComponent extends Component {
  @service store;
  @tracked display_per_page = 10;
  @tracked page = 1;
  @tracked columns = [];
  @tracked acronyms = [];
  @tracked has_next = true;
  @tracked has_prev = false;
  @tracked page_count = 1;
  @tracked sorting_column = null;
  @tracked sorting_ascending = null;
  @taskGroup({ drop: true }) changes;
  searchQueryWasEmpty = false;
  elementId = 'acronym-form-' + guidFor(this);

  /**
   * Set the component arguments to variables and update
   * the table.
   * @param  {...any} args The component arguments.
   */
  constructor(...args) {
    super(...args);
    let { columns } = this.args;
    // If a column is not enabled we remove the query.
    columns.forEach((column) => {
      if (!column.enabled || !('query' in column)) {
        column.query = null;
      }
    });
    this.columns = columns;

    // If the sorting_column is set we take it and put
    // the sorting_ascending to true.
    if (this.args.sorting_column) {
      this.sorting_column = this.args.sorting_column;
      this.sorting_ascending = true;
    }
    this.update.perform();
  }

  /**
   * This function fetchs the data from the backend with all
   * the parameters needed and is called when we press search,
   * when we change the sorting and change page settings.
   */
  @task({ drop: true })
  *update() {
    // Preparing the optional queries
    // Add the filters parameters
    let filter = {};
    this.columns.forEach((column) => {
      if (column.query && column.query.trim()) {
        filter[column.property] = column.query;
      }
    });
    // Add the sorting parameters.
    let sorting = {};
    if (this.sorting_column) {
      sorting['column'] = this.sorting_column;
    }
    if (this.sorting_ascending !== null) {
      sorting['ascending'] = this.sorting_ascending;
    }

    // Send the request with the parameters.
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
        this.page_count = results.meta.page_count;
        this.acronyms = results;
      });
    // Add a 300 ms timeout so we dont spam the backend.
    yield timeout(300);
  }

  /**
   * Change the number of acronym per page
   * @param {*} event Event of the select html object so we can get his value.
   */
  @task({ group: 'changes' })
  *changeDisplayPerPage(event) {
    let last_page = this.page;
    let last_display_per_page = this.display_per_page;
    this.display_per_page = parseInt(event.target.value);
    // Return to page 1.
    this.page = 1;
    // Update the table
    yield this.update.perform().catch(() => {
      // If it fails we go back to the old values.
      this.page = last_page;
      this.display_per_page = last_display_per_page;
    });
  }

  /**
   * Go to the selected page
   * @param {*} event Event of the select html object so we can get his value.
   */
  @task({ group: 'changes' })
  *changePage(event) {
    let last_page = this.page;
    this.page = parseInt(event.target.value);
    // Update the table. If it fails we go back to the old page.
    yield this.update.perform().catch(() => (this.page = last_page));
  }

  /**
   * Go to the next page
   */
  @task({ group: 'changes' })
  *next_page() {
    let last_page = this.page;
    this.page += 1;
    // Update the table. If it fails we go back to the old page.
    yield this.update.perform().catch(() => (this.page = last_page));
  }

  /**
   * Go to the previous page
   */
  @task({ group: 'changes' })
  *prev_page() {
    let last_page = this.page;
    this.page -= 1;
    // Update the table. If it fails we go back to the old page.
    yield this.update.perform().catch(() => (this.page = last_page));
  }

  /**
   * Go to the first page
   */
  @task({ group: 'changes' })
  *first_page() {
    let last_page = this.page;
    this.page = 1;
    // Update the table. If it fails we go back to the old page.
    yield this.update.perform().catch(() => (this.page = last_page));
  }

  /**
   * Go to the last page
   */
  @task({ group: 'changes' })
  *last_page() {
    let last_page = this.page;
    this.page = this.page_count;
    // Update the table. If it fails we go back to the old page.
    yield this.update.perform().catch(() => (this.page = last_page));
  }

  /**
   * Show/Hide the column of the button pressed
   * @param {*} columnProperty The column property name to Show/Hide
   */
  @task({ group: 'changes' })
  *toggleColumn(column) {
    column.enabled = !column.enabled;
    if (!column.enabled) {
      column.query = null;
    }
    // Change the columns
    yield this.changeColumns(this.columns);
  }

  /**
   * Remove the text within a query input if the 'X' button is pressed
   * @param {*} columnProperty The column property name to remove the query
   */
  @task({ group: 'changes' })
  *clearQuery(column) {
    column.query = null;
    // Change the columns
    this.changeColumns(this.columns);
    this.page = 1;
    yield this.update.perform();
  }

  /**
   * Update the table with the search queries.
   */
  @task({ group: 'changes' })
  *searchQuery() {
    let queryEmpty = true;
    for (const column of this.columns) {
      if (column.query && column.query.trim()) {
        queryEmpty = false;
        break;
      }
    }
    if (!this.searchQueryWasEmpty || !queryEmpty) {
      // Go back to page 1
      this.page = 1;
      yield this.update.perform();
    }
    this.searchQueryWasEmpty = queryEmpty;
  }

  /**
   * Change the sorting_column or/and the sorting_ascending variables
   * and update the table.
   * @param {string} column The column property name to remove the query
   */
  @task({ group: 'changes' })
  *changeSorting(column) {
    // If the user clicked on the column that is already activated
    if (this.sorting_column === column.property) {
      // If the column order is ascending, we set it to descending
      if (this.sorting_ascending) {
        this.sorting_ascending = false;
      }
      // If the column order is descending, we remove the column
      // from sorting.
      else {
        this.sorting_column = null;
        this.sorting_ascending = null;
      }
    }
    // If the column wasn't selected we activate it to asending.
    else {
      this.sorting_column = column.property;
      this.sorting_ascending = true;
    }
    // Update the table
    yield this.update.perform();
  }

  /**
   * If the user press the enter key we update the table.
   * @param {*} event The event of the key so we can know if
   * it's the enter key.
   */
  @action
  handleEnterKeyQuery(event) {
    // 13 is the keycode for the enter key
    if (event.keyCode === 13) {
      this.searchQuery.perform();
    }
  }

  /**
   * This function was made to update all related html attributes and component related to this.columns.
   * Since emberjs doesn't track array elements, we need to update the whole array pointer to update the template.
   * So we do a deep copy of the array.
   * @param {*} new_columns New version of the columns array
   */
  changeColumns(new_columns) {
    this.columns = JSON.parse(JSON.stringify(new_columns));
  }
}
