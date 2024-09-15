export async function promiseTuplify<T>(
  async_func: () => Promise<T>
): Promise<[T | null, Error | null]> {
  try {
    const res = await async_func()

    return [res, null]
  } catch (error) {
    return [null, error]
  }
}
