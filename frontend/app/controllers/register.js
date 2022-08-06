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

  @task({ drop: true })
  *createAccount(event) {
    event.preventDefault();
    this.errors = [];
    this.email1 = this.email1 ? this.email1.trim() : '';
    this.email2 = this.email2 ? this.email2.trim() : '';
    if (!this.email1 || !this.email2 || !this.password1 || !this.password2) {
      return;
    }
    if (this.email1 !== this.email2 || this.password1 !== this.password2) {
      this.errors = [{ detail: "Emails or Passwords doesn't match." }];
      return;
    }
    let email = this.email1;
    let password = this.password1;
    const response = yield fetch('api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

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
    } else {
      yield response.json().then((errorsData) => {
        this.errors = errorsData.errors;
      });
    }

    email = '';
    password = '';
    this.email1 = '';
    this.email2 = '';
    this.password1 = '';
    this.password2 = '';
  }

  willDestroy() {
    this.email1 = null;
    this.email2 = null;
    this.password1 = null;
    this.password2 = null;
  }
}
