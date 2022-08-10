import Controller from '@ember/controller';
import { service } from '@ember/service';
import { tracked } from '@glimmer/tracking';
import { task } from 'ember-concurrency';

export default class LoginController extends Controller {
  @service session;

  @tracked email;
  @tracked password;
  @tracked errors;

  /**
   * Try to login with the email and password.
   * @param {*} event Event of the submit button.
   * @returns
   */
  @task({ drop: true })
  *authenticate(event) {
    event.preventDefault();
    // If the email or the password are empty we return.
    this.email = this.email ? this.email.trim() : '';
    if (!this.email || !this.password) {
      return;
    }
    // Try to authenticate.
    yield this.session
      .authenticate('authenticator:token', this.email, this.password)
      .catch((errors) => {
        this.errors = errors.errors;
      });
    // Empty the email and password
    this.email = '';
    this.password = '';
  }

  /**
   * Attempt to empty the email and password because they
   * are sensitive data.
   */
  willDestroy() {
    this.email = null;
    this.password = null;
  }
}
