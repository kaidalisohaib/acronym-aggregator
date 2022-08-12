import { helper } from '@ember/component/helper';

/**
 * Return an array with items from start to end inclusively.
 */
export default helper(function range([start, end]) {
  start = parseInt(start);
  end = parseInt(end);
  var range = [];
  for (var i = start; i < end + 1; ++i) {
    range.push(i);
  }
  return range;
});
