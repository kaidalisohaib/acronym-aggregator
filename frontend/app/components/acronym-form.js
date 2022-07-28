import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';

export default class AcronymFormComponent extends Component {
  @tracked acronym = this.args.acronym.acronym;
  @tracked meaning = this.args.acronym.meaning;
  @tracked comment = this.args.acronym.comment;
  @tracked company = this.args.acronym.company;

  @action
  submitChanges() {
    console.log(this.acronym);
    console.log(this.meaning);
    console.log(this.comment);
    console.log(this.company);
    let oneAttributeIsContainsOnlySpace = false;
    if (!this.acronym.trim()) {
      this.acronym = '';
      oneAttributeIsContainsOnlySpace = true;
    }
    if (!this.meaning.trim()) {
      this.meaning = '';
      oneAttributeIsContainsOnlySpace = true;
    }
    if (!this.company.trim()) {
      this.company = '';
      oneAttributeIsContainsOnlySpace = true;
    }
    if (oneAttributeIsContainsOnlySpace) {
      return;
    }
    this.args.acronym.acronym = this.acronym;
    this.args.acronym.meaning = this.meaning;
    this.args.acronym.comment = this.comment;
    this.args.acronym.company = this.company;
    console.log(this.args.acronym.hasDirtyAttributes);
    console.log(this.args.acronym.changedAttributes());
    console.log('======================================');
    if (this.args.acronym.hasDirtyAttributes) {
      this.args.acronym.save();
    }
  }
}
