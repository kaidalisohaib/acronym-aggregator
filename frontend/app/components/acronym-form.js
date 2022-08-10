import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import { task } from 'ember-concurrency';
import { service } from '@ember/service';

export default class AcronymFormComponent extends Component {
  @service router;
  @tracked acronym = this.args.acronym.acronym;
  @tracked meaning = this.args.acronym.meaning;
  @tracked comment = this.args.acronym.comment;
  @tracked company = this.args.acronym.company;
  @tracked errors = [];
  @tracked canSubmit = false;

  /**
   * If the user started editing an acronym and went back to the
   * acronym/read-only page we reload the page to get the unmodified
   * propreties.
   * @param  {...any} args Component arguments.
   */
  constructor(...args) {
    super(...args);
    if (this.args.acronym.hasDirtyAttributes && !this.args.acronym.isNew) {
      window.location.reload();
    }
  }

  /**
   * This function apply the inputs to the variable
   * associated with them. If one of acronym, meaning
   * or company input is empty we disable the submit button.
   * @param {*} event Event of the submit button
   * @returns
   */
  @task
  *submitChanges(event) {
    event.preventDefault();
    this.canSubmit = false;
    // I trim the inputs so if one of them is empty
    // that means that it was full of white spaces.
    this.acronym = this.acronym ? this.acronym.trim() : '';
    this.meaning = this.meaning ? this.meaning.trim() : '';
    this.comment = this.comment ? this.comment.trim() : '';
    this.company = this.company ? this.company.trim() : '';

    // If any of those three column is empty we return.
    if (!this.acronym || !this.meaning || !this.company) {
      return;
    }

    // If the validation for empty inputs passes we
    // set the real attributes.
    this.args.acronym.acronym = this.acronym;
    this.args.acronym.meaning = this.meaning;
    this.args.acronym.comment = this.comment;
    this.args.acronym.company = this.company;

    // If there is no changed attributes we set the 'canSubmit'
    // variable to false to disable the submit button.
    yield (this.canSubmit = Object.keys(
      this.args.acronym.changedAttributes()
    ).length);
  }

  /**
   * This function is for the confirmation, just before
   * sending the data
   */
  @task({ drop: true })
  *confirmSubmit() {
    // Check if the acronym was changed.
    if (this.args.acronym.hasDirtyAttributes) {
      // Send the request to add/edit the acronym.
      yield this.args.acronym
        .save()
        .then((new_acronym) => {
          this.router.transitionTo('acronym', new_acronym);
        })
        .catch((error) => {
          this.errors = error.errors;
        });
    }
  }
}
