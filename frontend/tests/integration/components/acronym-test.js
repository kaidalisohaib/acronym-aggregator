import { module, test } from 'qunit';
import { setupRenderingTest } from 'frontend/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import moment from 'moment';

module('Integration | Component | acronym', function (hooks) {
  setupRenderingTest(hooks);

  hooks.beforeEach(function () {
    this.acronym_model = {
      id: 1,
      acronym: 'AKA',
      meaning: 'Also known as.',
      comment: 'A comment.',
      company: 'My company.',
      created_by: 'myemail@email.com',
      created_at: moment.utc(new Date()).format(),
      last_modified_by: 'anotheremail@email.com',
      last_modified_at: moment.utc(new Date()).format(),
    };
    this.columns = [
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
        enabled: true,
      },
      {
        name: 'created_at',
        property: 'created_at',
        enabled: true,
      },
      {
        name: 'last_modified_by',
        property: 'last_modified_by',
        enabled: true,
      },
      {
        name: 'last_modified_at',
        property: 'last_modified_at',
        enabled: true,
      },
    ];

    this.enabled_columns = 0;
    this.columns.forEach((column) => {
      if (column.enabled) {
        this.enabled_columns += 1;
      }
    });
  });

  test('it renders everything', async function (assert) {
    assert.expect(2 + this.enabled_columns - 1);

    await render(
      hbs`<Acronym @columns={{this.columns}} @acronym={{this.acronym_model}} />`
    );
    const row = this.element.firstElementChild;
    assert.dom(row).hasClass('acronym-row');

    assert.strictEqual(row.children.length, 9);

    for (const [index, td] of row.querySelectorAll('td').entries()) {
      const actual = td.innerText;
      const excpected = this.acronym_model[this.columns[index + 1].property];
      assert.strictEqual(actual, excpected);
    }
  });

  test('it renders only the id column', async function (assert) {
    assert.expect(3);

    this.columns.forEach((column) => {
      if (column.property !== 'id') {
        column.enabled = false;
      }
    });

    await render(
      hbs`<Acronym @columns={{this.columns}} @acronym={{this.acronym_model}} />`
    );
    const row = this.element.firstElementChild;
    assert.dom(row).hasClass('acronym-row');

    assert.strictEqual(row.children.length, 1);

    assert.dom(row.querySelector('th[scope="row"]')).exists();
  });

  test('it id column have the link to the acronym page', async function (assert) {
    assert.expect(1);

    await render(
      hbs`<Acronym @columns={{this.columns}} @acronym={{this.acronym_model}} />`
    );
    const row = this.element.firstElementChild;
    const link = row.querySelector('th[scope="row"]').firstElementChild;
    assert.strictEqual(link.getAttribute('href'), '/acronyms/1');
  });
});
