import Model, { attr } from '@ember-data/model';

export default class ReportModel extends Model {
  @attr('momentUTC') created_at;
}
