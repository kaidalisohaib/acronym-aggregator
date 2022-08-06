import JSONAPIAdapter from '@ember-data/adapter/json-api';
import { service } from '@ember/service';

export default class ApplicationAdapter extends JSONAPIAdapter {
  namespace = 'api';
  @service session;

  buildURL(...args) {
    return `${super.buildURL(...args)}`;
  }

  get headers() {
    let headers = {};
    if (this.session.isAuthenticated) {
      const simpleAuthSession = JSON.parse(
        localStorage.getItem('ember_simple_auth-session')
      );
      const accessToken = simpleAuthSession.authenticated.access_token;
      const authHeader = 'Bearer ' + accessToken;
      headers['Authorization'] = authHeader;
    }
    return headers;
  }

  handleResponse(status) {
    switch (status) {
      case 422:
      case 401:
        this.session.invalidate();
        break;
      default:
        break;
    }

    return super.handleResponse(...arguments);
  }
}
