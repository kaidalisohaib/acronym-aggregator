import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class CreateRoute extends Route {
  @service store;
  // @service session;

  // beforeModel(transition) {
  //   this.session.requireAuthentication(transition, 'login');
  // }

  async model() {
    return this.store.createRecord('acronym');
  }
}
