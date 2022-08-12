import { module, test } from 'qunit';
import { setupRenderingTest } from 'frontend/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';

module('Integration | Component | acronym-form', function (hooks) {
  setupRenderingTest(hooks);
  hooks.beforeEach(function () {
    this.acronym_model = {};
  });
  test('it renders with readonly=true', async function (assert) {
    await render(
      hbs`<AcronymForm @acronym={{this.acronym_model}} @readOnly={{true}}/>`
    );
    const main_div = this.element.firstElementChild;
    const form = main_div.querySelector('form');
    assert.dom(form.children[1].children[1]).hasAttribute('readonly');
    assert.dom(form.children[2].children[1]).hasAttribute('readonly');
    assert.dom(form.children[3].children[1]).hasAttribute('readonly');
    assert.dom(form.children[4].children[1]).hasAttribute('readonly');
    assert.dom(form.querySelector('button')).doesNotExist();
  });

  test('it renders with readonly=false', async function (assert) {
    await render(
      hbs`<AcronymForm @acronym={{this.acronym_model}} @readOnly={{false}}/>`
    );
    const main_div = this.element.firstElementChild;
    const form = main_div.querySelector('form');
    assert.dom(form.children[1].children[1]).doesNotHaveAttribute('readonly');
    assert.dom(form.children[2].children[1]).doesNotHaveAttribute('readonly');
    assert.dom(form.children[3].children[1]).doesNotHaveAttribute('readonly');
    assert.dom(form.children[4].children[1]).doesNotHaveAttribute('readonly');
    assert.dom(form.querySelector('button')).exists();
  });
});
