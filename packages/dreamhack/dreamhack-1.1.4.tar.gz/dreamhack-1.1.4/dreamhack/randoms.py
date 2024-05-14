class randoms():
  
  @staticmethod
  def random_string_generator(length): #type:ignore
    import random
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    master = ""
    for x in range(int(length)): #type:ignore
      master = master + random.choice(characters)
    return master 

  @staticmethod
  def random_number_in_range(min,max): #type:ignore
    import random
    try:
      return random.randrange(int(min), int(max)) #type:ignore
    except ValueError:
      raise ValueError('One or more of the numbers are invalid integers.') #type:ignore
    except Exception as e:
      raise e