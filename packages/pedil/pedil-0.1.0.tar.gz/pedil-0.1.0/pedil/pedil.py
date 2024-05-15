import sympy

class PEDIL:
    def __init__(self, base_prime_limit=10**6):  # Base array size up to 1 million
        self.base_primes = list(sympy.primerange(0, base_prime_limit))
        #print(f"Initialized with {len(self.base_primes)} base primes.")
        self.prime_cache = {}

    def generate_prime_id(self, pedil_notation):
        """
        Generate a unique prime ID based on the PEDIL notation.
        :param pedil_notation: A string representing the PEDIL notation, e.g., '1,1'
        :return: A unique prime number as the ID
        """
        #print(f"Generating prime ID for notation: {pedil_notation}")
        levels = pedil_notation.split(',')
        prime_index = 0
        base_length = len(self.base_primes)
        for i, level in enumerate(levels):
            prime_index += int(level) * (base_length ** (len(levels) - i - 1))
        #print(f"Calculated prime_index: {prime_index}")
        if prime_index >= len(self.base_primes):
            self.extend_prime_array(prime_index)
        #print(f"Generated prime ID: {self.base_primes[prime_index]}")
        return self.base_primes[prime_index]

    def extend_prime_array(self, required_index):
        """
        Extend the base prime array to accommodate higher indices.
        :param required_index: The required index to extend the array to
        """
        current_max = len(self.base_primes)
        additional_primes_needed = required_index - current_max + 1
        #print(f"Extending prime array to accommodate index: {required_index} (adding {additional_primes_needed} primes)")

        next_prime_start = self.base_primes[-1] + 1
        new_primes = []
        chunk_size = 100000  # Manageable chunk size for generating primes
        while len(new_primes) < additional_primes_needed:
            next_prime_end = next_prime_start + chunk_size
            #print(f"Generating primes in range: {next_prime_start} to {next_prime_end}")
            primes_generated = list(sympy.primerange(next_prime_start, next_prime_end))
            new_primes.extend(primes_generated)
            next_prime_start = next_prime_end
            #print(f"Primes generated in this iteration: {len(primes_generated)}")
            #print(f"Total primes generated so far: {len(new_primes)}")

            if not primes_generated:
                raise RuntimeError("Failed to generate new primes.")

        self.base_primes.extend(new_primes[:additional_primes_needed])
        #print(f"Extended prime array to {len(self.base_primes)} primes.")
        #print(f"New primes added: {new_primes[:additional_primes_needed]}")

    def get_or_create_prime_id(self, alias):
        """
        Retrieve or generate a unique prime ID for a given alias.
        :param alias: A string alias for the ID
        :return: A unique prime number as the ID
        """
        if alias in self.prime_cache:
            #print(f"Found cached prime ID for alias '{alias}': {self.prime_cache[alias]}")
            return self.prime_cache[alias]
        prime_id = self.generate_prime_id(alias)
        self.prime_cache[alias] = prime_id
        #print(f"Cached prime ID for alias '{alias}': {prime_id}")
        return prime_id
