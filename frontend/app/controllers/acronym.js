import Controller from '@ember/controller';
import { task } from 'ember-concurrency';
import { service } from '@ember/service';

export default class AcronymController extends Controller {
  @service router;
  @service session;

  /**
   * Delete the current acronym if authenticated.
   * @returns
   */
  @task({ drop: true })
  *deleteAcronym() {
    if (!this.session.isAuthenticated) {
      return;
    }
    yield this.model
      .destroyRecord()
      .then(() => {
        this.router.transitionTo('index');
      })
      .catch(() => {
        this.model.rollbackAttributes();
      });
  }
}
