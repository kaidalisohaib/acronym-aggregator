import Controller from '@ember/controller';
import { tracked } from '@glimmer/tracking';

export default class IndexController extends Controller {
  columns = [
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
      enabled: false,
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
      name: 'last_modified_at',
      property: 'last_modified_at',
      enabled: false,
    },
    {
      name: 'last_modified_by',
      property: 'last_modified_by',
      enabled: false,
    },
  ];
}
