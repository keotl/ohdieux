package ca.ligature.ohdieux.utils

extension [A, B](a: A) 
    infix def |>(f: A => B): B = f(a)
