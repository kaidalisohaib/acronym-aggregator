import Controller from '@ember/controller';

export default class IndexController extends Controller {
  /**
   * All the columns with their information.
   * - name is the display text in the table header
   * - proprety is the name of the model attribute
   * - enabled is if the column is shown or not
   * - query is the search query of the column
   */
  columns = [
    {
      name: 'ID',
      property: 'id',
      enabled: true,
    },
    {
      name: 'acronym',
      property: 'acronym',
      enabled: true,
    },
    {
      name: 'meaning',
      property: 'meaning',
      enabled: true,
    },
    {
      name: 'comment',
      property: 'comment',
      enabled: true,
    },
    {
      name: 'company',
      property: 'company',
      enabled: true,
    },
    {
      name: 'created_by',
      property: 'created_by',
      enabled: false,
    },
    {
      name: 'created_at',
      property: 'created_at',
      enabled: false,
    },
    {
      name: 'last_modified_by',
      property: 'last_modified_by',
      enabled: false,
    },
    {
      name: 'last_modified_at',
      property: 'last_modified_at',
      enabled: false,
    },
  ];
}
