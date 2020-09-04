---
title: "Swift Tour (Basic Syntax)"
layout: post
date: 2019-08-30 
tag:
- Swift
category: blog
author: ingerchao
description: The notes of swift learning
---



```swift
//
//  main.swift
//  helloswift
//
//  Created by 赵琦 on 2019/9/1.
//  Copyright © 2019 inger. All rights reserved.
//

import Foundation

print("Hello, World!")

var myVariable = 42
myVariable = 50
let myConstant = 42

let implicitInt = 70
let implicitDouble = 70.0
let expilicitDouble : Double = 70.0
let expilicitFloat : Float = 70.0

let label = "the width is: "
let width = 94
let widthLabel = label + String(width)

let apples = 3
let oranges = 5
let appleSummary = "I have \(apples) apples."
let fruitSummary = "I have \(apples + oranges) pieces of fruits."
let olds : Float = 21.6
let name = "Inger"
let hello = "Hello, \(olds) year old " + name
print(hello)

let quotation = """
I said "I have \(apples) apples."
And then I said "I have \(apples + oranges) pieces of fruits."
"""
print(quotation)

var shoppingList = ["catfish", "water", "tulips" ]
shoppingList[1] = "bottle of water"

var occupations = [
    "Malcolm" : "Captain",
    "Kaylee" : "Mechanic",
]
occupations["Jayne"] = "Public Relations"

shoppingList.append("blue paint")
print(shoppingList)
print(occupations)

// create empty array dictionary by the initializer syntax
let emptyArray = [String]()
let emptyDictiong = [String : Float]()
// if type information can be inferred, we can wirte an empty array by [] or an empty dictionary by[:

shoppingList = []
occupations = [:]
print(shoppingList)
print(occupations)

// control flow
let individualScores = [10, 20, 98, 55]
var teamScore = 0
for score in individualScores{
    if score > 50 {
        teamScore += 3
    } else {
        teamScore += 1
    }
}
print(teamScore)

var optionalString : String? = "Hello"
// An optional value either contains a value or contains nil to indicate that a value is missing
print(optionalString == nil)

var optionalName : String? = nil
var greeting = "Hello!"
if let n = optionalName {
    greeting = "Hello, \(n)"
} else {
    print("the optional is nil")
}
print(greeting)

let nickName : String? = nil
let fullName : String = "Inger Chao"
//  If the optional value is missing, the default value is used instead.
let informalGreeting = "hi \(nickName ?? fullName)"
print(informalGreeting)

// remove default will error for that switch must be exhaustive
let vegetable = "red apple"
switch vegetable {
case "celery":
    print("add some raisins and make ants on a log.")
case "a", "b":
    print("a or b")
//Notice how let can be used in a pattern to assign the value that matched the pattern to a constant.
case let x where x.hasSuffix("apple"):
    print("It's a spcy \(x)")
default:
    print("everyting tasts good")
}

let interestingNumbers = [
    "Prime" : [2, 3, 5, 7, 11, 13],
    "Fibonacci" : [1, 1, 2, 3, 5, 8],
    "Square" : [1, 4, 9, 16, 25],
]
var largest = 0
var largestKind = ""
for (kind, numbers) in interestingNumbers{
    for number in numbers {
        if number > largest {
            largest = number
            largestKind = kind
        }
    }
}
print(largestKind + " " + String(largest))

var n = 2
while n < 100 {
    n *= 2
}
print(n)

var m = 2
repeat {
    m *= 2
}while m < 100
print(m)

var total = 0
// keep an index a loop bu using ..< to make a range of indexs
for i in 0..<4 {
    total += i
}
print(total)

// function and closures
// Use -> to separate the parameter names and types from the function’s return type.
func greet(person: String, day: String) -> String {
    return "Hello \(person), today is \(day)"
}
print(greet(person:" inger", day: "8.31"))
// write _ to use no argument label, or wirte a custom argument label before the parameter name
func greet2(_ person: String, on day: String) -> String {
    return "Hello \(person), todya is \(day)"
}
print(greet2("Inger", on: "2019.8.30"))

// use a tuple to make a compound value
// the elements of a tuple can be referred to either by name or by number

func calculate(scores: [Int]) -> (min: Int, max: Int, sum: Int) {
    var min = scores[0]
    var max = scores[0]
    var sum = 0
    
    for score in scores {
        if score > max {
            max = score
        } else if score < min {
            min = score
        }
         sum += score
    }
    return (min, max, sum)
}
let statistics = calculate(scores: [5, 3, 100, 3, 9])
print(statistics.sum)
print(statistics.1) // statistics max

// function can be nested
// nested function have access to variables that declared in outer function
func returnFifteen() -> Int {
    var y = 10
    func add() {
        y += 5
    }
    return y
}
print(returnFifteen())

// Functions are a first-class type.
// A function can return another function as its value

func makeIncrementer() -> ((Int) -> Int) {
    func addOne(number: Int) -> Int {
        return 1 + number
    }
    return addOne
}

var increment = makeIncrementer()
print(increment(7))

func hasAnyMatched(list: [Int], condition: (Int) -> Bool) -> Bool {
    for item in list {
        if condition(item) {
            return true
        }
    }
    return false
}

func lessThanTen(number: Int) -> Bool {
    return number < 10
}

var numbers = [20, 19, 7, 12]
print(hasAnyMatched(list: numbers, condition: lessThanTen(number:)))
// closure without a name by surrounding code with braces ({})
numbers.map({(number : Int) -> Int in
    let result = 3*number
    return result
})

let mappedNumbers = numbers.map({ number in 3 * number})
print(mappedNumbers)
// When a closure is the only argument to a function, you can omit the parentheses entirely.
let sortedNumbers = numbers.sorted { $0 > $1 }
print(sortedNumbers)

class Shape {
    var numberOfSides = 0
    func simpleDescription() -> String {
        return "A shape with \(simpleDescription) sides.)"
    }
    let angle = 4
    func angleDescription() -> String {
        return "A shape with \(angle) angles."
    }
}

var shape = Shape()
shape.numberOfSides = 7
var shapeDescription = shape.simpleDescription()

class NameShape {
    var numberOfSides: Int = 0
    var name: String
    // use init to create an initializer to set up the class when an instance is created
    // use deinit to create an deinitizlizer
    init(name: String){
        self.name = name
    }
    func simpleDescription() -> String {
        return "The shape \(name) has \(numberOfSides) sides."
    }
}

// Subclasses
// 1. setting the value of properties that the subclass declares
// 2. calling the superclass's initializer
// 3. changing the value of properties defined by the superclass
class Square : NameShape {
    var sideLength: Double
    
    // properties can have a getter and setter
    var perimiter: Double {
        get {
            return Double(numberOfSides) * sideLength
        }
        set {
            sideLength = newValue / 4.0
        }
    }
    
    init(sideLength: Double, name: String) {
        self.sideLength = sideLength
        super.init(name: name)
        numberOfSides = 4
    }
    func area() -> Double {
        return sideLength * sideLength
    }
    
    override func simpleDescription() -> String {
        return "A square with sides of length \(sideLength)"
    }
}

let square = Square(sideLength: 5.2, name: "test square")
print(square.area())
print(square.simpleDescription())
square.perimiter = 20
print(square.sideLength)
// provide code that is run before and after setting a new value, use willSet and didSet
class TriangleAndSquare {
    var square: Square {
        willSet {
            square.sideLength = newValue.sideLength
        }
    }
    init(size: Double, name : String) {
        square = Square(sideLength: size, name: name)
    }
}

enum Rank: Int {
    case ace = 1
    case two, three, four, five, six, seven, eight, nine, ten
    case jack, queen, king
    
    func simpleDescription() -> String {
        switch self {
        case .ace:
            return "ace"
        case .jack:
            return "jack"
        case .queen:
            return "queen"
        case .king:
            return "king"
        default:
            return String(self.rawValue)
        }
    }
}
let ace = Rank.ace
let aceRawValue = ace.rawValue
let kingRawValue = Rank.king.rawValue
print(ace) // ace
print(aceRawValue)
print(kingRawValue) //3

if let convertedRank = Rank(rawValue: 13) {
    let thirenteenDescription = convertedRank.simpleDescription()
    print(thirenteenDescription)
}

enum ServerResponse {
    case result(String, String)
    case failure(String)
}

let success = ServerResponse.result("6:00 am", "8:09 pm")
let failure = ServerResponse.failure("oue of cheese.")

switch success {
case let .result(sunrise, sunset):
    print("sunrise is at \(sunrise), and sunset is at \(sunset)")
case let .failure(message):
    print("Failure:... \(message)")
}

// create a sturcture
/* the difference betweent structures and classes is that
sutructures are always copied when they are passed aruound in your code,
 but classes are passed by reference */
struct Card {
    var rank: Rank
    var number : String
    func simpleDescription() -> String{
        return "The \(number) student ranks \(rank.simpleDescription())."
    }
}
let threeOfCards = Card(rank: .three, number: "stu1")
let threeOfCardsDescription = threeOfCards.simpleDescription()
print(threeOfCardsDescription)

// Protocol and Generics would describ at next specfic blog.

```

-------

