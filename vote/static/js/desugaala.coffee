apiCall = (opts) -> _.defaults {}, opts, 
  type: 'POST'
  headers:
    "X-CSRFToken": $(":input[name='csrfmiddlewaretoken']").val()
    "Content-Type": "application/json"

serializeBallot = ->
  ballot = []

  for categoryEl in $('.category')
    $category = $(categoryEl)
    category = $category.data 'category'

    console?.log 'category', category

    options = []

    for optionEl in $category.find('li')
      $option = $(optionEl)
      if $option.is '.deadline'
        console?.log 'deadline'
      else
        option = $option.data 'option'
        console?.log ' - option', option
        options.push option
    
    ballot.push {category, options} if options.length > 0

  url: '/vote'
  data: JSON.stringify ballot

$ ->
  $('.category').sortable().disableSelection()

  _loggedIn = $('#id_username').asEventStream('change')
    .merge($('#id_username').asEventStream('keyup'))
    .merge($('#id_password').asEventStream('change'))
    .merge($('#id_password').asEventStream('keyup'))
    .throttle(1500)
    .map ->
      username: $('#id_username').val()
      password: $('#id_password').val()
    .filter (v) ->
      v.username and v.password
    .map (data) ->
      url: '/login'
      data: JSON.stringify data
    .map(apiCall)
    .map((v) -> v.result == 'ok')
    .toProperty(false)

  $('#send-button').asEventStream('click')
    .filter(_loggedIn)
    .map(serializeBallot)
    .map(apiCall)
    .ajax()
    .onValue (v) -> console?.log '/vote response', v