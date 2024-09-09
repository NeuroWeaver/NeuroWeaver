with Component() as main:
    with Component() as producer_thread:
        n = 0
        b  = 'test'
        a = 'n_gen' + b
        while True:
            componentProduce(a, n)
            n = n + 1
            if n == 1000:
                break
    producer_thread()
    with Component() as consumer_thread:
        while True:
            n = componentConsume('n_gentest')
            print(f'consumed {n}')
            if n == 999:
                break
    consumer_thread()
main()