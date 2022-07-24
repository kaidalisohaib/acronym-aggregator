import { module, test } from 'qunit';
import { setupRenderingTest } from 'frontend/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';

module('Integration | Helper | range', function (hooks) {
  setupRenderingTest(hooks);

  // TODO: Replace this with your real tests.
  test('it renders', async function (assert) {
    this.set('start', '1');
    this.set('end', '10');

    await render(hbs`{{range this.start this.end}}`);
    assert.dom(this.element).containsText('1,');
    assert.dom(this.element).containsText('2,');
    assert.dom(this.element).containsText('5,');
    assert.dom(this.element).containsText('9,');
    assert.dom(this.element).containsText('10,');
  });
});
