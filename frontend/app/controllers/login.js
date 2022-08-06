import Controller from '@ember/controller';
import { service } from '@ember/service';
import { tracked } from '@glimmer/tracking';
import { task } from 'ember-concurrency';

export default class LoginController extends Controller {
  @service session;

  @tracked email;
  @tracked password;
  @tracked errors;

  @task({ drop: true })
  *authenticate(event) {
    event.preventDefault();
    this.email = this.email ? this.email.trim() : '';
    if (!this.email || !this.password) {
      return;
    }
    yield this.session
      .authenticate('authenticator:token', this.email, this.password)
      .catch((errors) => {
        this.errors = errors.errors;
      });
    this.email = '';
    this.password = '';
  }

  willDestroy() {
    this.email = null;
    this.password = null;
  }
}
