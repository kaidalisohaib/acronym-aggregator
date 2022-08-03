import Controller from '@ember/controller';
import download from 'downloadjs';
import { service } from '@ember/service';
import { task, timeout } from 'ember-concurrency';
import { tracked } from '@glimmer/tracking';

export default class ReportsController extends Controller {
  @service store;
  @tracked errors;

  @task({ drop: true })
  *downloadVersion(version) {
    console.log(version);
    // download(`/api/reports/${version}`, `all_acronyms_v${version}.zip`);
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

  @task({ drop: true })
  *createReport() {
    yield this.store
      .createRecord('report')
      .save()
      .catch((error) => {
        this.errors = error.errors;
      });
    yield timeout(2000);
  }
}
