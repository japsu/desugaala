Bacon.EventStream.prototype.ajax = function() {
  return this["switch"](function(params) { return Bacon.fromPromise($.ajax(params)) })
}