function loadMeals(filter = "all") {
  const savedMeals = JSON.parse(localStorage.getItem("currentRecipes")) || [];
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
      updateMealSlot(currentSlotId, selectedMeal);
      modal.style.display = "none";
    });
  });
  // ... rest of your existing click handlers ...
  console.log(" Filtered Meals:", filteredMeals);
}

// New function to update the slot
function updateMealSlot(slotId, meal) {
  const slot = document.querySelector(`[data-slot-id="${slotId}"]`);
  
  // Remove 'empty' class if present
  slot.classList.remove('empty');
  
  // Update slot content
  slot.innerHTML = `
    <div class="meal-time">${getMealTime(slotId)}</div>
    <div class="meal-content">
      <img src="${meal.image}" alt="${meal.title}" class="w-10 h-10 object-cover inline mr-2">
      ${meal.title}
    </div>
    <button class="add-meal">✏️ Edit</button>
  `;
  
  // Reattach click handler
  slot.querySelector('.add-meal').addEventListener('click', (e) => {
    currentSlotId = slotId;
    modal.style.display = 'flex';
  });
  
  // Update localStorage
  saveToMealPlan(slotId, meal);
}

// Helper functions
function getMealTime(slotId) {
  // Customize based on your slot naming
  return slotId.includes('lunch') ? 'Lunch' : 'Dinner';
}

function saveToMealPlan(slotId, meal) {
  const mealPlan = JSON.parse(localStorage.getItem('mealPlan')) || {};
  mealPlan[slotId] = meal;
  localStorage.setItem('mealPlan', JSON.stringify(mealPlan));
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
  updateNutrientSummary();
});
// Simple script to show/hide modals (non-functional prototype)
let currentSlotId = null; // Track which slot we're editing

// Update your existing add-meal handler
document.querySelectorAll(".add-meal").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    currentSlotId = e.target.closest(".meal-slot").dataset.slotId;
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
  // This is a placeholder - replace with actual calculation based on meals
  // You would sum up nutrients from all meals for the day
  return {
    calories: Math.floor(Math.random() * 500) + 1500, // Random between 1500-2000
    protein: Math.floor(Math.random() * 30) + 40, // Random between 40-70g
    carbs: Math.floor(Math.random() * 100) + 150, // Random between 150-250g
    fat: Math.floor(Math.random() * 30) + 40, // Random between 40-70g
    fiber: Math.floor(Math.random() * 15) + 10, // Random between 10-25g
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

// Call this function whenever meals are updated
updateNutrientSummary();
