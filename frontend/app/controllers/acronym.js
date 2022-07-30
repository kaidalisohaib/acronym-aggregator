import Controller from '@ember/controller';
import { task } from 'ember-concurrency';
import { service } from '@ember/service';

export default class AcronymController extends Controller {
  @service router;

  @task({ drop: true })
  *deleteAcronym() {
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
