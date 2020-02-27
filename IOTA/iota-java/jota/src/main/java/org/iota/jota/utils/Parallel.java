package org.iota.jota.utils;

import java.util.Collection;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Parallel {

    private static final int NUM_CORES = Runtime.getRuntime().availableProcessors();
    private static final ExecutorService forPool = Executors.newFixedThreadPool(NUM_CORES * 2, new NamedThreadFactory("Parallel.For"));

    /**
     * @param elements
     * @param operation
     * @param <T>
     * @throws InterruptedException 
     */
    public static <T> void of(final Iterable<T> elements, final Operation<T> operation) throws InterruptedException {
        forPool.invokeAll(createCallables(elements, operation));
    }

    /**
     * @param elements
     * @param operation
     * @param <T>
     * @return a collection of tasks which are currently performing
     */
    public static <T> Collection<Callable<Void>> createCallables(Iterable<T> elements, Operation<T> operation) {
        List<Callable<Void>> callables = new LinkedList<>();
        for (final T elem : elements) {
            callables.add(new Callable<Void>() {
                @Override
                public Void call() {
                    operation.perform(elem);
                    return null;
                }
            });
        }

        return callables;
    }

    /**
     * @param <T>
     */
    public interface Operation<T> {
        void perform(T pParameter);
    }
}