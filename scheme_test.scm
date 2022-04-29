/# some notes: if you want to have multiple expressions not wrapped in an overarching set of () you need to add a ; between them
additionally, since * don't play nice with regex comments are made using the form shown here. As you can see, it's not perfect, but it's comming along#/;
(define add (lambda (x y) (+ x y)));
(print (add 1 2))