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
      query: null,
    },
    {
      name: 'acronym',
      property: 'acronym',
      enabled: true,
      query: null,
    },
    {
      name: 'meaning',
      property: 'meaning',
      enabled: true,
      query: null,
    },
    {
      name: 'comment',
      property: 'comment',
      enabled: true,
      query: null,
    },
    {
      name: 'company',
      property: 'company',
      enabled: true,
      query: null,
    },
    {
      name: 'created_by',
      property: 'created_by',
      enabled: false,
      query: null,
    },
    {
      name: 'created_at',
      property: 'created_at',
      enabled: false,
      query: null,
    },
    {
      name: 'last_modified_by',
      property: 'last_modified_by',
      enabled: false,
      query: null,
    },
    {
      name: 'last_modified_at',
      property: 'last_modified_at',
      enabled: false,
      query: null,
    },
  ];
}
