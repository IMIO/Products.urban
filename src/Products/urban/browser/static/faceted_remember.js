/* Remember select_to_list choices in localStorage */
(function ($) {
  "use strict";

  if (typeof Faceted === "undefined") {
    return;
  }

  var PREFIX = "urban.faceted.";

  function storageKey(wid) {
    return PREFIX + window.location.pathname + "." + wid;
  }

  function read(key) {
    try {
      return window.localStorage.getItem(key);
    } catch (e) {
      return null;
    }
  }

  function write(key, value) {
    try {
      if (value) {
        window.localStorage.setItem(key, value);
      } else {
        window.localStorage.removeItem(key);
      }
    } catch (e) {
      // localStorage unavailable (private mode, blocked storage...)
    }
  }

  function restoreInHash(wid, value) {
    var state = $.bbq.getState();
    if (state.hasOwnProperty(wid)) {
      // The URL explicitly sets this criterion: it wins
      return;
    }
    state[wid] = value;
    var hash = "#" + $.param(state, true);
    if (window.history && window.history.replaceState) {
      window.history.replaceState(null, "", hash);
    }
  }

  $(Faceted.Events).bind(Faceted.Events.INITIALIZE, function () {
    $(".faceted-remember").each(function () {
      var $select = $(this).find("select");
      var wid = $select.attr("id");
      if (!wid) {
        return;
      }
      var key = storageKey(wid);

      $select.bind("change", function () {
        write(key, $(this).val());
      });

      var stored = read(key);
      if (!stored) {
        return;
      }
      var exists = $select.find("option").filter(function () {
        return this.value === stored;
      }).length;
      if (!exists) {
        return;
      }

      $select.val(stored);
      Faceted.Query[wid] = [stored];
      if (window.location.hash) {
        restoreInHash(wid, stored);
      }
    });
  });
})(jQuery);