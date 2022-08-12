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
    assert.dom(this.element).hasText('1,2,3,4,5,6,7,8,9,10');
  });
});
