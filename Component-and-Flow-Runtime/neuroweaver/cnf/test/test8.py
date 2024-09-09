
with Component() as main:
    mycount = 0
    with Component(state=[count]) as comp_A:
        print(count)  # Persistent state
        if True:
            print(count)
    comp_A(mycount)

main()
