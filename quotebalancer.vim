if !has('python3')
  finish
endif

function! QuoteBalancer()
  py3file 'quotebalancer.py'
endfunc


command! QuoteBalancer call QuoteBalancer()
