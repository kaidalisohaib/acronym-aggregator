import Route from '@ember/routing/route';
import { service } from '@ember/service';
import { tracked } from '@glimmer/tracking';

export default class IndexRoute extends Route {
  @service store;

  queryParams = {
    display_per_page: {
      refreshModel: true,
    },
  };

  async model(params) {
    return this.store.query('acronym', params);
  }
}
