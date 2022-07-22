import { module, test } from 'qunit';
import { setupRenderingTest } from 'frontend/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';

module('Integration | Component | acronyms', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<Acronyms />`);

    assert.dom(this.element).hasText('');

    // Template block usage:
    await render(hbs`
      <Acronyms>
        template block text
      </Acronyms>
    `);

    assert.dom(this.element).hasText('template block text');
  });
});
