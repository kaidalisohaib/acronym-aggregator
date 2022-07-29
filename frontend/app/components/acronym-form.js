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

  @task
  *submitChanges() {
    this.acronym = this.acronym ? this.acronym.trim() : '';
    this.meaning = this.meaning ? this.meaning.trim() : '';
    this.comment = this.comment ? this.comment.trim() : '';
    this.company = this.company ? this.company.trim() : '';

    if (!this.acronym || !this.meaning || !this.company) {
      return;
    }

    this.args.acronym.acronym = this.acronym;
    this.args.acronym.meaning = this.meaning;
    this.args.acronym.comment = this.comment;
    this.args.acronym.company = this.company;
    if (this.args.acronym.hasDirtyAttributes) {
      yield this.args.acronym
        .save()
        .then((new_acronym) => {
          this.router.transitionTo('acronym', new_acronym);
        })
        .catch((error) => {
          console.log('Error: ', error);
          this.errors = error.errors;
        });
      console.log(this.args.acronym.errors);
    }
  }
}
