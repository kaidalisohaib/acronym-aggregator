import { module, test } from 'qunit';
import { setupTest } from 'frontend/tests/helpers';

module('Unit | Controller | reports', function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test('it exists', function (assert) {
    let controller = this.owner.lookup('controller:reports');
    assert.ok(controller);
  });
});
