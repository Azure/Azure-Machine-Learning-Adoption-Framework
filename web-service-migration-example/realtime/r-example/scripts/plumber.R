# plumber.R

library(caret)

mtcar_ridge_model <- readRDS("model.rds")

#* Liveness check
#* @get /live
function() {
  "alive"
}

#* Readiness check
#* @get /ready
function() {
  "ready"
}

#* predict a car's miles per gallon with information of a car
#* @param cyl, number of cylinders, possible values 4,6,8 
#* @param disp, possible values 71-460  
#* @param hp, Gross horsepower, possible value in 52-335
#* @param drat, Rear axle ratio, possible value in 3.00-4.93
#* @param wt, Weight (1000 lbs),possible values in 1.513-5.424
#* @param qsec, 1/4 mile time,possible values 14.5 -22.9
#* @param vs, V/s, possible values "0","1"
#* @param am, Transmission (0 = automatic, 1 = manual)
#* @param gear,  Number of forward gears,possible values 3,4,5
#* @param carb, Number of carburetors,possible values 1,2,3,4,6,8
#* @post /score
function(cyl,disp,hp,drat,wt,qsec,vs,am,gear,carb){
  newdata <- data.frame(
    cyl=as.numeric(cyl),
    disp=as.numeric(disp),
    hp=as.numeric(hp),
    drat=as.numeric(drat),
    wt=as.numeric(wt),
    qsec=as.numeric(qsec),
    vs=as.numeric(vs),
    am=as.numeric(am),
    gear=as.numeric(gear),
    carb=as.numeric(carb)
  )
  prediction <- predict(mtcar_ridge_model,newdata)
  
  return(prediction)
  }