import Controller from '@ember/controller';
import { tracked } from '@glimmer/tracking';
import { task } from 'ember-concurrency';

export default class UploadController extends Controller {
  @tracked skippedRows = [];
  @tracked errors = [];
  @tracked addedRows = 0;
  @tracked totalRows = 0;

  @task({ drop: true })
  *uploadCSV(file) {
    this.errors = [];
    this.skippedRows = [];
    this.addedRows = 0;
    this.totalRows = 0;
    yield file
      .upload('/api/upload')
      .then((response) => {
        response.json().then((data) => {
          this.skippedRows = data['skippedRows'];
          this.addedRows = data['addedRows'];
          this.totalRows = data['totalRows'];
        });
        alert('Successfully uploaded the file to the server.');
      })
      .catch((error) => {
        error.json().then((data) => {
          this.errors = data['errors'];
        });
        file.state = 'aborted';
      });
  }
}
