import EmberRouter from '@ember/routing/router';
import config from 'frontend/config/environment';

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

Router.map(function () {
  this.route('index', { path: '/' });
  this.route('index');
  this.route('acronym', { path: '/acronyms/:acronym_id' });
  this.route('edit', { path: '/edit/:acronym_id' });
  this.route('create');
  this.route('login');
  this.route('reports');
  this.route('upload');
});
