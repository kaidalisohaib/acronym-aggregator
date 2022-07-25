import Model, { attr } from '@ember-data/model';

export default class AcronymModel extends Model {
  @attr('string') acronym;
  @attr('string') meaning;
  @attr('string') comment;
  @attr('string') company;
  @attr('string') created_by;
  @attr('string') last_modified_by;
  @attr('momentUTC') last_modified_at;
  @attr('momentUTC') created_at;
}
