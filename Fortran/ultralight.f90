program ultralight
    implicit none
    real :: m, c, E
    call getarg(1, m)
    c = 299792458.0
    E = m * c**2
    print *, E
end program ultralight


