import { helper } from '@ember/component/helper';

export default helper(function range([start, end]) {
  var range = [];
  for (var i = start; i < end + 1; ++i) {
    range.push(i);
  }
  return range;
});
