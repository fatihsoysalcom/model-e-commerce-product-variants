import itertools

class ProductVariantManager:
    def __init__(self, base_product_name, attributes_config):
        self.base_product_name = base_product_name
        self.attributes_config = attributes_config
        self.variants = {} # Stores variant_id -> {attributes, sku, price, stock}
        self._generate_variants()

    def _generate_variants(self):
        # Extract attribute names and their possible values
        attribute_names = list(self.attributes_config.keys())
        attribute_values_lists = [self.attributes_config[name] for name in attribute_names]

        # This is the core concept: each combination of attributes forms a unique product variant
        for i, combination in enumerate(itertools.product(*attribute_values_lists)):
            variant_attributes = dict(zip(attribute_names, combination))
            variant_id = f"{self.base_product_name.lower().replace(' ', '-')}-{i+1}"
            sku = self._generate_sku(variant_attributes)

            # Assign default price and stock for demonstration purposes
            price = 29.99 + (i * 0.5) 
            stock = 10 + (i % 5)      

            self.variants[variant_id] = {
                "attributes": variant_attributes,
                "sku": sku,
                "price": price,
                "stock": stock
            }

    def _generate_sku(self, attributes):
        # A simple SKU generation based on attributes to ensure uniqueness per variant
        sku_parts = [self.base_product_name[:3].upper()]
        for attr_name in sorted(attributes.keys()): # Sort for consistent SKU generation
            sku_parts.append(str(attributes[attr_name])[:3].upper().replace(' ', ''))
        return "-".join(sku_parts)

    def get_variant_by_attributes(self, target_attributes):
        for variant_id, variant_data in self.variants.items():
            if variant_data["attributes"] == target_attributes:
                return variant_id, variant_data # Return both ID and data
        return None, None

    def update_stock(self, variant_id, quantity_change):
        # Demonstrates managing stock for an individual variant
        if variant_id in self.variants:
            self.variants[variant_id]["stock"] += quantity_change
            print(f"Updated stock for {variant_id}. New stock: {self.variants[variant_id]['stock']}")
            return True
        print(f"Variant {variant_id} not found.")
        return False

    def display_all_variants(self):
        print(f"\n--- All Variants for {self.base_product_name} ---")
        for variant_id, data in self.variants.items():
            attr_str = ", ".join([f"{k}: {v}" for k, v in data['attributes'].items()])
            print(f"ID: {variant_id}")
            print(f"  Attributes: {attr_str}")
            print(f"  SKU: {data['sku']}")
            print(f"  Price: ${data['price']:.2f}")
            print(f"  Stock: {data['stock']}")
            print("-" * 20)

# --- Example Usage ---
if __name__ == "__main__":
    # Define the attributes for a "Kurti" product, as discussed in the article
    kurti_attributes = {
        "Color": ["Red", "Blue", "Green"],
        "Size": ["S", "M", "L", "XL"],
        "Fabric": ["Cotton", "Rayon"],
        "Pattern": ["Floral", "Geometric"]
    }

    # Initialize the variant manager for "Kurti"
    kurti_manager = ProductVariantManager("Kurti", kurti_attributes)

    # Display all generated variants, showing each as a distinct product
    kurti_manager.display_all_variants()

    # Demonstrate finding a specific variant by its attributes
    print("\n--- Searching for a specific variant ---")
    target_attrs = {"Color": "Blue", "Size": "M", "Fabric": "Cotton", "Pattern": "Floral"}
    found_variant_id, found_variant_data = kurti_manager.get_variant_by_attributes(target_attrs)

    if found_variant_id:
        print(f"Found variant for {target_attrs}:")
        print(f"  ID: {found_variant_id}, SKU: {found_variant_data['sku']}, Price: ${found_variant_data['price']:.2f}, Stock: {found_variant_data['stock']}")
        # Demonstrate stock update for this specific variant
        kurti_manager.update_stock(found_variant_id, -2)
    else:
        print(f"Variant with attributes {target_attrs} not found.")

    # Show the updated stock for that variant
    print("\n--- Displaying a specific variant after stock update ---")
    _, found_variant_data_after_update = kurti_manager.get_variant_by_attributes(target_attrs)
    if found_variant_data_after_update:
        print(f"Updated stock for {target_attrs}: {found_variant_data_after_update['stock']}")

    # Try to update stock for a non-existent variant
    kurti_manager.update_stock("non-existent-variant-id", 5)
