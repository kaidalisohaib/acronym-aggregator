import Controller from '@ember/controller';
import { tracked } from '@glimmer/tracking';

export default class IndexController extends Controller {
  columns = [
    {
      name: 'acronym',
      property: 'acronym',
    },
    {
      name: 'meaning',
      property: 'meaning',
    },
    {
      name: 'comment',
      property: 'comment',
    },
    {
      name: 'company',
      property: 'company',
    },
    {
      name: 'created_by',
      property: 'created_by',
    },
    {
      name: 'created_at',
      property: 'created_at',
    },
    {
      name: 'last_modified_at',
      property: 'last_modified_at',
    },
    {
      name: 'last_modified_by',
      property: 'last_modified_by',
    },
  ];
}
