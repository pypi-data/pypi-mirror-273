# Function to create a new string with n copies of a given string
def repeat_string(string, n)
    return string * n
  end
  
  # Function to print the extension of a file given its filename
  def get_file_extension(filename)
    return File.extname(filename)
  end
  
  # Function to print the user's first and last name in reverse order
  def reverse_name(first_name, last_name)
    return "#{last_name} #{first_name}"
  end
  
  # Function to retrieve the total marks from a hash containing subject names and marks
  def total_marks(marks_hash)
    total = 0
    marks_hash.each_value { |marks| total += marks }
    return total
  end
  
  # Function to check if two temperatures are out of bounds
  def out_of_bounds?(temp1, temp2)
    return (temp1 < 0 && temp2 > 100) || (temp1 > 100 && temp2 < 0)
  end
  
  # Main program
  puts "1. Create a new string with n copies of a given string"
  puts repeat_string("hello", 3)  # Output: hellohellohello
  puts "\n"
  
  puts "2. Print the extension of a file given its filename"
  puts get_file_extension("example.txt")  # Output: .txt
  puts "\n"
  
  puts "3. Print the user's first and last name in reverse order"
  puts reverse_name("John", "Doe")  # Output: Doe John
  puts "\n"
  
  puts "4. Retrieve the total marks from a hash containing subject names and marks"
  student_marks = { "Maths" => 90, "Science" => 85, "English" => 88 }
  puts total_marks(student_marks)  # Output: 263
  puts "\n"
  
  puts "5. Check if two temperatures are out of bounds"
  puts out_of_bounds?(10, 105)  # Output: true
  puts out_of_bounds?(-5, 90)   # Output: false
  