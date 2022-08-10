import Controller from '@ember/controller';
import { tracked } from '@glimmer/tracking';
import { task } from 'ember-concurrency';

export default class UploadController extends Controller {
  @tracked skippedRows = [];
  @tracked errors = [];
  @tracked addedRows = 0;
  @tracked totalRows = 0;
  @tracked lastUploadedFilename = '';

  /**
   * Try to send the csv file to the backend.
   * @param {*} file The file to send.
   */
  @task({ drop: true })
  *uploadCSV(file) {
    this.errors = [];
    this.skippedRows = [];
    this.addedRows = 0;
    this.totalRows = 0;

    // Get the ember simple auth dictionary from the localStorage.
    const simpleAuthSession = JSON.parse(
      localStorage.getItem('ember_simple_auth-session')
    );
    // Get the JWT token.
    const accessToken = simpleAuthSession.authenticated.access_token;
    // Authorization header.
    const authHeader = 'Bearer ' + accessToken;
    // Send the request.
    yield file
      .upload('/api/upload', { headers: { Authorization: authHeader } })
      // If the response went well.
      .then((response) => {
        response.json().then((data) => {
          this.skippedRows = data['skippedRows'];
          this.addedRows = data['addedRows'];
          this.totalRows = data['totalRows'];
        });
        this.lastUploadedFilename = file.name;
        alert('Successfully uploaded the file to the server.');
      })
      // If the response responded with an error.
      .catch((error) => {
        error.json().then((data) => {
          this.errors = data['errors'];
        });
        file.state = 'aborted';
      });
  }
}
