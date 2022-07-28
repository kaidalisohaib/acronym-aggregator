import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class EditRoute extends Route {
  @service store;

  async model(params) {
    return this.store.findRecord('acronym', params.acronym_id);
  }
}
