import EmberRouter from '@ember/routing/router';
import config from 'frontend/config/environment';

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

Router.map(function () {
  this.route('index', { path: '' });
  this.route('acronym', { path: '/acronyms/:acronym_id' });
  this.route('login');
  this.route('register');
  this.route('reports');
  this.route('authenticated', { path: '/auth' }, function () {
    this.route('edit', { path: '/edit/:acronym_id' });
    this.route('create');
    this.route('upload');
  });
});
