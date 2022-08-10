import Controller from '@ember/controller';
import download from 'downloadjs';
import { service } from '@ember/service';
import { task, timeout } from 'ember-concurrency';
import { tracked } from '@glimmer/tracking';

export default class ReportsController extends Controller {
  @service store;
  @service session;
  @tracked errors;

  /**
   * This function triggers the download of a zip file.
   * @param {*} version The version number.
   */
  @task({ drop: true })
  *downloadVersion(version) {
    var x = new XMLHttpRequest();
    x.open('GET', `/api/reports/${version}`, true);
    x.responseType = 'blob';
    x.onload = function (e) {
      let filename = x
        .getResponseHeader('Content-Disposition')
        .split('filename=')[1]
        .split(';')[0];
      download(e.target.response, filename, e.target.response.type);
    };
    yield x.send();
  }

  /**
   * Send a request to the backend to create a new report.
   * @returns
   */
  @task({ drop: true })
  *createReport() {
    // Only if authenticated
    if (!this.session.isAuthenticated) {
      return;
    }
    // Send the request.
    let new_record = this.store.createRecord('report');
    yield new_record.save().catch((error) => {
      new_record.rollbackAttributes();
      this.errors = error.errors;
    });
    // Apply a timeout before calling this function again
    // to not spam the backend.
    yield timeout(2000);
  }
}
