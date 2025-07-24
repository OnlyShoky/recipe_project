function loadMeals(filter = "all") {
  const savedMeals = JSON.parse(localStorage.getItem("favoriteRecipes")) || [];
  const filteredMeals = filter === "all" ? savedMeals : savedMeals.filter((meal) => meal.type === filter);

  const emptyMessage = document.getElementById("empty-meals-message");
  const mealContainer = document.getElementById("meal-options");

  // Toggle empty state
  if (filteredMeals.length === 0) {
    emptyMessage.style.display = "block";
    mealContainer.style.display = "none";
  } else {
    emptyMessage.style.display = "none";
    mealContainer.style.display = "grid"; // or your preferred layout
  }

  // Render meals
  mealContainer.innerHTML = filteredMeals
    .map(
      (meal) => `
    <div class="meal-type" data-id="${meal.id}">
      <img src="${meal.image}" alt="${meal.title}" class="w-12 h-12 object-cover mx-auto" />
      <div class="truncate ... sm:max-w-xs lg:max-w-sm">${meal.title}</div>
      <div class="small">
        ${formatTime(meal.total_time)} • ${Math.round(meal.nutrition?.calories || 0)} cal
      </div>
    </div>
  `
    )
    .join("");

  // Add this to your loadMeals function (after rendering meals)
  mealContainer.querySelectorAll(".meal-type").forEach((mealEl) => {
    mealEl.addEventListener("click", () => {
      const mealId = mealEl.dataset.id;
      const selectedMeal = filteredMeals.find((m) => m.id == mealId);
      updateMealSlot(currentSlotID, selectedMeal);
      modal.style.display = "none";
    });
  });
}

// New function to update the slot
function updateMealSlot(slotID, meal) {
  const slot = document.querySelector(`[data-slot-id="${slotID}"]`);

  // Remove 'empty' class if present
  slot.classList.remove("empty");

  // Update slot content
  slot.innerHTML = `
        <div class="meal-time">${getMealTime(slotID)}</div>
        <a href="/recipes/${meal.id}/" class="transform transition-transform hover:scale-105">
            <div class="meal-content">${meal.title}</div>
        </a>
        <button class="add-meal">✏️ Edit</button>
    `;

  // Reattach click handler
  slot.querySelector(".add-meal").addEventListener("click", (e) => {
    currentSlotID = slotID;
    modal.style.display = "flex";
  });

  // Update localStorage
  saveToMealPlan(slotID, meal);
}

// Helper functions
function getMealTime(slotId) {
  if (slotId >= 1 && slotId <= 7) return "Breakfast";
  if (slotId >= 8 && slotId <= 14) return "Lunch";
  if (slotId >= 15 && slotId <= 21) return "Dinner";
  // Customize based on your slot naming
  return "breakfast";
}

function saveToMealPlan(slotId, meal) {
  const mealPlan = JSON.parse(localStorage.getItem("mealPlan")) || {};
  mealPlan[slotId] = meal;
  localStorage.setItem("mealPlan", JSON.stringify(mealPlan));
}

const modal = document.getElementById("meal-modal");
const modalObserver = new MutationObserver(() => {
  if (modal.style.display === "flex") {
    loadMeals();
  }
});
modalObserver.observe(modal, { attributes: true });

// Add this helper function (put it above your loadMeals function)
function formatTime(time) {
  // Handle null/undefined
  if (time == null) return "Time not specified";

  // If it's already a number in minutes (most common case)
  if (typeof time === "number") {
    if (time < 60) return `${time} min`;
    const hours = Math.floor(time / 60);
    const mins = time % 60;
    return `${hours} hr${hours !== 1 ? "s" : ""}${mins > 0 ? ` ${mins} min` : ""}`;
  }

  // If it's a time string like "01:30:00"
  if (typeof time === "string" && time.includes(":")) {
    const parts = time.split(":");
    const hours = parseInt(parts[0]);
    const mins = parseInt(parts[1]);

    if (hours > 0) {
      return `${hours} hr${hours !== 1 ? "s" : ""}${mins > 0 ? ` ${mins} min` : ""}`;
    }
    return `${mins} min`;
  }

  // Fallback for unexpected formats
  return "Time varies";
}

function openProfileModal() {
  document.getElementById("profile-modal").style.display = "flex";
}

function closeProfileModal() {
  document.getElementById("profile-modal").style.display = "none";
}

function closeGrocerySidebar() {
  document.getElementById("grocery-sidebar").style.display = "none";
}

document.getElementById("profile-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const sex = this.sex.value;
  const age = parseFloat(this.age.value);
  const height = parseFloat(this.height.value);
  const weight = parseFloat(this.weight.value);
  const activity = parseFloat(this.activity.value);

  let bmr;
  if (sex === "male") {
    bmr = 10 * weight + 6.25 * height - 5 * age + 5;
  } else {
    bmr = 10 * weight + 6.25 * height - 5 * age - 161;
  }

  const calorieIntake = Math.round(bmr * activity);
  document.getElementById("calorie-result").textContent = "Estimated Daily Calorie Intake: " + calorieIntake + " kcal";

  // Store nutrient targets based on profile
  const nutrientTargets = {
    calories: calorieIntake,
    protein: { target: Math.round(weight * 1.6), max: Math.round(weight * 2) }, // 1.6-2g per kg of body weight
    carbs: { target: Math.round((calorieIntake * 0.5) / 4), max: Math.round((calorieIntake * 0.6) / 4) }, // 50-60% of calories
    fat: { target: Math.round((calorieIntake * 0.25) / 9), max: Math.round((calorieIntake * 0.35) / 9) }, // 25-35% of calories
    fiber: { target: 25, max: 40 },
  };

  localStorage.setItem("nutrientTargets", JSON.stringify(nutrientTargets));
});
// Simple script to show/hide modals (non-functional prototype)
let currentSlotID = null; // Track which slot we're editing

// Update your existing add-meal handler
document.querySelectorAll(".add-meal").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    currentSlotID = e.target.closest(".meal-slot").dataset.slotId;
    document.getElementById("meal-modal").style.display = "flex";
  });
});

document.querySelector(".close-modal").addEventListener("click", () => {
  document.getElementById("meal-modal").style.display = "none";
});

document.getElementById("generate-grocery").addEventListener("click", () => {
  document.getElementById("grocery-sidebar").style.display = "block";
});

// Add these functions to your existing script section
function openPreferencesModal() {
  document.getElementById("preferences-modal").style.display = "flex";
  loadPreferences();
}

function closePreferencesModal() {
  document.getElementById("preferences-modal").style.display = "none";
}

function loadPreferences() {
  // Load saved preferences from localStorage if available
  const savedPrefs = JSON.parse(localStorage.getItem("mealPreferences")) || {};

  // Set protein preferences
  document.querySelectorAll('input[name="protein"]').forEach((checkbox) => {
    checkbox.checked = savedPrefs.proteins ? savedPrefs.proteins.includes(checkbox.value) : checkbox.checked;
  });

  // Set carb preferences
  document.querySelectorAll('input[name="carb"]').forEach((checkbox) => {
    checkbox.checked = savedPrefs.carbs ? savedPrefs.carbs.includes(checkbox.value) : checkbox.checked;
  });

  // Set other preferences
  document.querySelectorAll('input[name="preference"]').forEach((checkbox) => {
    checkbox.checked = savedPrefs.other ? savedPrefs.other.includes(checkbox.value) : false;
  });

  // Load banned ingredients
  const bannedList = document.getElementById("banned-ingredients-list");
  bannedList.innerHTML = "";
  if (savedPrefs.bannedIngredients) {
    savedPrefs.bannedIngredients.forEach((ingredient) => {
      const item = document.createElement("div");
      item.className = "banned-ingredient-item";
      item.innerHTML = `
          ${ingredient}
          <span class="remove-ingredient" onclick="removeBannedIngredient('${ingredient}')">×</span>
        `;
      bannedList.appendChild(item);
    });
  }
}

function savePreferences() {
  const preferences = {
    proteins: Array.from(document.querySelectorAll('input[name="protein"]:checked')).map((c) => c.value),
    carbs: Array.from(document.querySelectorAll('input[name="carb"]:checked')).map((c) => c.value),
    other: Array.from(document.querySelectorAll('input[name="preference"]:checked')).map((c) => c.value),
    bannedIngredients: Array.from(document.querySelectorAll(".banned-ingredient-item")).map((item) => item.textContent.replace("×", "").trim()),
  };

  localStorage.setItem("mealPreferences", JSON.stringify(preferences));
  closePreferencesModal();
  alert("Preferences saved! These will be used when generating your meal plan.");
}

function addBannedIngredient() {
  const input = document.getElementById("new-banned-ingredient");
  const ingredient = input.value.trim();

  if (ingredient) {
    const bannedList = document.getElementById("banned-ingredients-list");
    const item = document.createElement("div");
    item.className = "banned-ingredient-item";
    item.innerHTML = `
        ${ingredient}
        <span class="remove-ingredient" onclick="removeBannedIngredient('${ingredient}')">×</span>
      `;
    bannedList.appendChild(item);
    input.value = "";
  }
}

function removeBannedIngredient(ingredient) {
  const items = document.querySelectorAll(".banned-ingredient-item");
  items.forEach((item) => {
    if (item.textContent.replace("×", "").trim() === ingredient) {
      item.remove();
    }
  });
}

// Nutrient tracking functions
// Replace your existing nutrient tracking functions with:
function updateNutrientSummary() {
  // Get the user's daily targets from profile or localStorage
  const dailyTargets = JSON.parse(localStorage.getItem("nutrientTargets")) || {
    calories: 2000,
    protein: { target: 50, max: 100 },
    carbs: { target: 250, max: 300 },
    fat: { target: 65, max: 80 },
    fiber: { target: 25, max: 40 },
  };

  // Get all nutrient summary slots
  const nutrientSlots = document.querySelectorAll(".nutrient-summary");

  // For each day in the week
  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

  nutrientSlots.forEach((slot, index) => {
    const day = days[index];
    const dayNutrients = calculateDayNutrients(day);

    const caloriesProgress = Math.min(100, (dayNutrients.calories / dailyTargets.calories) * 100);
    let caloriesClass = "nutrient-optimal";
    if (dayNutrients.calories < dailyTargets.calories * 0.8) caloriesClass = "nutrient-warning";
    else if (dayNutrients.calories > dailyTargets.calories * 1.2) caloriesClass = "nutrient-danger";

    slot.innerHTML = `
      <div class="nutrient-day">
        <div class="nutrient-item">Calories: ${dayNutrients.calories}kcal</div>
        <div class="nutrient-bar">
          <div class="nutrient-progress ${caloriesClass}" style="width: ${caloriesProgress}%"></div>
        </div>
        <div class="nutrient-item">Protein: ${dayNutrients.protein}g</div>
        <div class="nutrient-bar">
          <div class="nutrient-progress ${getNutrientClass(dayNutrients.protein, dailyTargets.protein)}" 
               style="width: ${Math.min(100, (dayNutrients.protein / dailyTargets.protein.max) * 100)}%"></div>
        </div>
      </div>
    `;
  });
}

function getNutrientClass(value, target) {
  if (value < target.target * 0.8) return "nutrient-warning";
  if (value > target.max) return "nutrient-danger";
  return "nutrient-optimal";
}

function calculateDayNutrients(day) {
  // Get stored meals from localStorage
  const weeklyMeals = JSON.parse(localStorage.getItem('weeklyMeals')) || { meals: {} };
  
  // Initialize totals
  const totals = {
    calories: 0,
    protein: 0,
    carbs: 0,
    fat: 0,
    fiber: 0
  };

  // Meal types to check
  const mealTypes = ['breakfast', 'lunch', 'dinner'];

  // Sum nutrients for all meals of the day
  mealTypes.forEach(mealType => {
    const mealKey = `${day}_${mealType}`;
    const meal = weeklyMeals.meals[mealKey];
    
    console.log(`Calculating ${day} ${mealType} nutrients - Meal title: ${meal.title}, calories: ${meal.nutrition.calories}`);
    
    if (meal && meal.nutrition) {
      totals.calories += meal.nutrition.calories || 0;
      totals.protein += meal.nutrition.protein || 0;
      totals.carbs += meal.nutrition.carbs || 0;
      totals.fat += meal.nutrition.fat || 0;
      totals.fiber += meal.nutrition.fiber || 0;
    }
  });

  // Round values
  console.log(`Day ${day} total nutrients: ${totals.calories}`);
  return {
    calories: Math.round(totals.calories),
    protein: Math.round(totals.protein),
    carbs: Math.round(totals.carbs),
    fat: Math.round(totals.fat),
    fiber: Math.round(totals.fiber)
  };
}

function createNutrientItem(name, value, target, unit) {
  let progressClass = "";
  let progressWidth = 0;

  if (typeof target === "object") {
    // For nutrients with target and max (like protein)
    progressWidth = Math.min(100, (value / target.max) * 100);
    if (value < target.target * 0.8) progressClass = "nutrient-warning";
    else if (value > target.max) progressClass = "nutrient-danger";
    else progressClass = "nutrient-optimal";
  } else {
    // For simple targets (like calories)
    progressWidth = Math.min(100, (value / target) * 100);
    if (value < target * 0.8) progressClass = "nutrient-warning";
    else if (value > target * 1.2) progressClass = "nutrient-danger";
    else progressClass = "nutrient-optimal";
  }

  return `
    <div class="nutrient-item">
      <div>${name}: ${value}${unit}</div>
      <div class="nutrient-bar">
        <div class="nutrient-progress ${progressClass}" style="width: ${progressWidth}%"></div>
      </div>
    </div>
  `;
}



// Generate Weekly Meals

document.getElementById("generate-weekly-meals").addEventListener("click", async function () {
  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
  const mealTypes = ["breakfast", "lunch", "dinner"];
  
  try {
    // Clear previous storage
    localStorage.removeItem('weeklyMeals');
    
    // Create storage object
    const weeklyMeals = {
      generatedAt: new Date().toISOString(),
      meals: {}
    };

    const response = await fetch(`/generate-meals`);
    const data = await response.json();
    let slotID = 1;

    for (const mealType of mealTypes) {
      for (const day of days) {
        if (data.meals && data.meals.length > 0) {
          const slot = findMealSlot(day, mealType);
          if (slot) {
            const meal = data.meals[slotID-1];
            
            // Store meal data with day and mealType as composite key
            weeklyMeals.meals[`${day}_${mealType}`] = {
              ...meal,
              day: day,
              mealType: mealType,
              slotID: slotID
            };
            
            chargeMealSlot(slot, meal, slotID);
            slotID++;
          }
        }
      }
    }
    
    // Save to localStorage
    localStorage.setItem('weeklyMeals', JSON.stringify(weeklyMeals));

    // Update nutrient summary
    updateNutrientSummary();
    
  } catch (error) {
    console.error("Error generating meals:", error);
  }
});

// Helper function - you need to implement based on your slot structure
function findMealSlot(day, mealType) {
  // This depends on how you structure your DOM
  // Example: Find element with data-day="Monday" and data-meal="breakfast"
  return document.querySelector(`[data-day="${day}"][data-meal-type="${mealType}"]`);
}

function chargeMealSlot(slotElement, mealData, slotID) {
  // Completely rebuild the slot HTML from scratch every time
  slotElement.innerHTML = `
        <div class="meal-time">${getMealTime(slotID)}</div>
        <a href="/recipes/${mealData.id}/" class="transform transition-transform hover:scale-105">
            <div class="meal-content">${mealData.title}</div>
        </a>
        <button class="add-meal">✏️ Edit</button>
    `;

  // Reattach click handler
  slotElement.querySelector(".add-meal").addEventListener("click", (e) => {
    currentSlotID = slotID;
    modal.style.display = "flex";
  });

  // Remove empty class if it exists
  slotElement.classList.remove("empty");

  // Helper function
  function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }
}
