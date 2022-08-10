import Controller from '@ember/controller';
import { tracked } from '@glimmer/tracking';
import { service } from '@ember/service';
import { task } from 'ember-concurrency';

export default class RegisterController extends Controller {
  @service session;
  @service router;

  @tracked email1;
  @tracked email2;
  @tracked password1;
  @tracked password2;
  @tracked errors;

  /**
   * Try to register with a email and password.
   * @param {*} event Event of the submit button.
   * @returns
   */
  @task({ drop: true })
  *createAccount(event) {
    event.preventDefault();
    this.errors = [];
    // If one of the four field is empty we return.
    this.email1 = this.email1 ? this.email1.trim() : '';
    this.email2 = this.email2 ? this.email2.trim() : '';
    if (!this.email1 || !this.email2 || !this.password1 || !this.password2) {
      return;
    }
    // If the two emails or the two passwords are not equal we return.
    if (this.email1 !== this.email2 || this.password1 !== this.password2) {
      this.errors = [{ detail: "Emails or Passwords doesn't match." }];
      return;
    }
    let email = this.email1;
    let password = this.password1;
    // Send the request.
    const response = yield fetch('api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    // If the backend successfully created the user we
    // automatically login.
    if (response.ok) {
      this.session
        .authenticate('authenticator:token', email, password)
        .then(() => {
          this.router.transitionTo('index');
        })
        .catch((errors) => {
          this.errors = errors.errors;
        });
      email = '';
      password = '';
    }
    // If there was an error we show the errors to the user.
    else {
      yield response.json().then((errorsData) => {
        this.errors = errorsData.errors;
      });
    }

    // Attempt to empty any sensitive data.
    email = '';
    password = '';
    this.email1 = '';
    this.email2 = '';
    this.password1 = '';
    this.password2 = '';
  }

  /**
   * Attempt to empty any sensitive data.
   */
  willDestroy() {
    this.email1 = null;
    this.email2 = null;
    this.password1 = null;
    this.password2 = null;
  }
}
