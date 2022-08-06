import Route from '@ember/routing/route';
import { service } from '@ember/service';
export default class UploadRoute extends Route {
  @service session;
}
